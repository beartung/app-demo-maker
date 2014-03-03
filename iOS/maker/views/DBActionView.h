//
//  DBActionView.h
//  maker
//
//  Created by Bear on 2/23/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DBAction.h"

@interface DBActionView : UIView

@property (nonatomic, strong) NSString * pid;
@property (nonatomic, strong) NSString * refer;
@property (nonatomic, strong) DBAction * action;

- (id)initWithFrame:(CGRect)frame pageId:(NSString *)pid referId:(NSString *)refer action:(DBAction *)action;

@end
