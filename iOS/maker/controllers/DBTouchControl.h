//
//  DBTouchControl.h
//  maker
//
//  Created by Bear on 2/23/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol DBTouchControl <NSObject>

-(void)onTap:(UITapGestureRecognizer *)tap;
-(void)onSlide:(UITapGestureRecognizer *)tap;
-(void)twoFingersTwoTaps;

@end
